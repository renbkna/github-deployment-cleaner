"use client"

import { useState } from "react";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { AlertCircle, CheckCircle, GitBranch, Trash2 } from "lucide-react";

interface Deployment {
  id: string;
  ref: string;
  state: string;
  created_at: string;
}

interface Message {
  category: string;
  message: string;
}

export default function GitHubDeployments() {
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [username, setUsername] = useState<string>("");
  const [repo, setRepo] = useState<string>("");

  const fetchDeployments = async () => {
    if (!username || !repo) {
      setMessages([{ category: "error", message: "Please provide both GitHub username and repository name." }]);
      return;
    }
    try {
      const response = await fetch(`/api/deployments?username=${encodeURIComponent(username)}&repo=${encodeURIComponent(repo)}`);
      if (!response.ok) {
        throw new Error("Failed to fetch deployments");
      }
      const data = await response.json();
      setDeployments(data);
      setMessages([]);
    } catch (error) {
      console.error("Error fetching deployments:", error);
      setMessages([{ category: "error", message: "Failed to fetch deployments" }]);
    }
  };

  const markInactive = async (id: string) => {
    if (!username || !repo) {
      setMessages([{ category: "error", message: "Please provide both GitHub username and repository name." }]);
      return;
    }
    try {
      const response = await fetch(
        `/api/deployments/${id}/mark_inactive?username=${encodeURIComponent(username)}&repo=${encodeURIComponent(repo)}`,
        { method: "POST" }
      );
      if (!response.ok) {
        throw new Error("Failed to mark deployment as inactive");
      }
      setMessages([{ category: "success", message: `Deployment ${id} marked as inactive` }]);
      fetchDeployments(); // Refresh list
    } catch (error) {
      console.error("Error marking deployment as inactive:", error);
      setMessages([{ category: "error", message: `Failed to mark deployment ${id} as inactive` }]);
    }
  };

  const deleteDeployment = async (id: string) => {
    if (!username || !repo) {
      setMessages([{ category: "error", message: "Please provide both GitHub username and repository name." }]);
      return;
    }
    if (confirm(`Are you sure you want to delete deployment ${id}?`)) {
      try {
        const response = await fetch(
          `/api/deployments/${id}?username=${encodeURIComponent(username)}&repo=${encodeURIComponent(repo)}`,
          { method: "DELETE" }
        );
        if (!response.ok) {
          throw new Error("Failed to delete deployment");
        }
        setMessages([{ category: "success", message: `Deployment ${id} deleted successfully` }]);
        fetchDeployments(); // Refresh list
      } catch (error) {
        console.error("Error deleting deployment:", error);
        setMessages([{ category: "error", message: `Failed to delete deployment ${id}` }]);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Card className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-800">GitHub Deployments</h1>
            <div className="mt-4 flex flex-col sm:flex-row sm:items-center sm:space-x-4">
              <input
                type="text"
                placeholder="GitHub Username"
                className="p-2 border rounded"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="text"
                placeholder="Repository Name"
                className="p-2 border rounded mt-2 sm:mt-0"
                value={repo}
                onChange={(e) => setRepo(e.target.value)}
              />
              <Button variant="outline" size="sm" onClick={fetchDeployments}>
                Fetch Deployments
              </Button>
            </div>
          </div>

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`bg-${msg.category === "success" ? "green" : "red"}-100 border-l-4 border-${
                msg.category === "success" ? "green" : "red"
              }-500 text-${msg.category === "success" ? "green" : "red"}-700 p-4 mb-4`}
              role="alert"
            >
              <p className="font-bold">{msg.category === "success" ? "Success" : "Error"}</p>
              <p>{msg.message}</p>
            </div>
          ))}

          {deployments.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Ref</TableHead>
                  <TableHead>State</TableHead>
                  <TableHead>Created At</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {deployments.map((deployment) => (
                  <TableRow key={deployment.id}>
                    <TableCell>{deployment.id}</TableCell>
                    <TableCell className="flex items-center">
                      <GitBranch className="mr-2 h-4 w-4" />
                      {deployment.ref}
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          deployment.state === "success"
                            ? "success"
                            : deployment.state === "failure"
                            ? "destructive"
                            : "default"
                        }
                      >
                        {deployment.state === "success" ? (
                          <CheckCircle className="mr-1 h-3 w-3" />
                        ) : (
                          <AlertCircle className="mr-1 h-3 w-3" />
                        )}
                        {deployment.state || "unknown"}
                      </Badge>
                    </TableCell>
                    <TableCell>{new Date(deployment.created_at).toLocaleString()}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm" onClick={() => markInactive(deployment.id)}>
                          Mark Inactive
                        </Button>
                        <Button variant="destructive" size="sm" onClick={() => deleteDeployment(deployment.id)}>
                          <Trash2 className="mr-1 h-4 w-4" />
                          Delete
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="p-6 text-center text-gray-500">No deployments found.</div>
          )}
        </Card>
      </div>
    </div>
  );
}

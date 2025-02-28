import React from "react";
import {
  MessageSquare,
  Upload,
  BookOpen,
  Github,
  Star,
  GitFork,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="bg-gradient-to-b from-primary/10 to-background py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center space-y-6">
            <h1 className="text-5xl font-bold tracking-tight">
              Knowledge Based AI System
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              A revolutionary AI-powered platform for knowledge analysis,
              transcription, and intelligent chat interactions.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Button size="lg" onClick={() => navigate("/upload")}>
                <Upload className="mr-2 h-5 w-5" />
                Try Demo
              </Button>
              <Button size="lg" variant="outline">
                <Github className="mr-2 h-5 w-5" />
                View on GitHub
              </Button>
            </div>
            <div className="flex items-center justify-center gap-4 text-muted-foreground">
              <div className="flex items-center gap-1">
                <Star className="h-4 w-4" />
                <span>1.2k stars</span>
              </div>
              <div className="flex items-center gap-1">
                <GitFork className="h-4 w-4" />
                <span>234 forks</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="p-6 space-y-4">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <Upload className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">Smart Upload</h3>
              <p className="text-muted-foreground">
                Drag & drop your vlogs with real-time processing status and
                smart content extraction.
              </p>
            </Card>

            <Card className="p-6 space-y-4">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <MessageSquare className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">AI Chat</h3>
              <p className="text-muted-foreground">
                Engage with an AI that understands your vlog content and
                provides meaningful insights.
              </p>
            </Card>

            <Card className="p-6 space-y-4">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                <BookOpen className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold">Knowledge Base</h3>
              <p className="text-muted-foreground">
                Build a searchable knowledge repository from your vlog content
                automatically.
              </p>
            </Card>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <div className="py-16 bg-muted/50">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold mb-8">Technical Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <h3 className="text-xl font-semibold">Core Technologies</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>• React with TypeScript for type-safe development</li>
                <li>• Tailwind CSS with ShadcnUI for modern styling</li>
                <li>• Vite for lightning-fast builds</li>
                <li>• Real-time video processing and analysis</li>
                <li>• Advanced AI models for content understanding</li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="text-xl font-semibold">Key Features</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>• Drag & drop file uploads with progress tracking</li>
                <li>• Real-time transcription and content analysis</li>
                <li>• AI-powered chat interface for content queries</li>
                <li>• Automatic knowledge base generation</li>
                <li>• Dark mode support with theme customization</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

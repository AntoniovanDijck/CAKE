import React from "react";
import { Progress } from "../ui/progress";
import { Card } from "../ui/card";
import { CheckCircle2, Loader2, Upload } from "lucide-react";

interface ProgressIndicatorProps {
  status?: "idle" | "uploading" | "processing" | "complete";
  progress?: number;
  fileName?: string;
}

const ProgressIndicator = ({
  status = "idle",
  progress = 0,
  fileName = "example-video.mp4",
}: ProgressIndicatorProps) => {
  const getStatusIcon = () => {
    switch (status) {
      case "uploading":
        return <Upload className="animate-bounce h-5 w-5 text-blue-500" />;
      case "processing":
        return <Loader2 className="animate-spin h-5 w-5 text-yellow-500" />;
      case "complete":
        return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      default:
        return null;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "uploading":
        return "Uploading...";
      case "processing":
        return "Processing...";
      case "complete":
        return "Complete!";
      default:
        return "Ready to upload";
    }
  };

  return (
    <Card className="w-full p-6 space-y-4 bg-white dark:bg-gray-800">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <p className="text-sm font-medium text-gray-700 dark:text-gray-200">
              {fileName}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {getStatusText()}
            </p>
          </div>
        </div>
        <span className="text-sm font-medium text-gray-700 dark:text-gray-200">
          {progress}%
        </span>
      </div>

      <Progress value={progress} className="h-2 transition-all" />
    </Card>
  );
};

export default ProgressIndicator;

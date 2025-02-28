import React from "react";
import { NavLink } from "react-router-dom";
import { Home, MessageSquare, Upload, BookOpen, Sun, Moon } from "lucide-react";
import { cn } from "@/lib/utils";
import { useTheme } from "@/lib/ThemeProvider";
import { Button } from "@/components/ui/button";

const Sidebar = () => {
  const { theme, toggleTheme } = useTheme();

  const navItems = [
    { icon: Home, label: "Home", path: "/" },
    { icon: MessageSquare, label: "Chat", path: "/chat" },
    { icon: Upload, label: "Upload", path: "/upload" },
    { icon: BookOpen, label: "Knowledge", path: "/knowledge" },
  ];

  return (
    <div className="h-screen w-16 border-r bg-background flex flex-col items-center py-4">
      <div className="flex-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "w-12 h-12 flex items-center justify-center rounded-lg mb-2 transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                isActive
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground",
              )
            }
            title={item.label}
          >
            <item.icon className="w-5 h-5" />
          </NavLink>
        ))}
      </div>

      <Button
        variant="ghost"
        size="icon"
        className="w-12 h-12 rounded-lg"
        onClick={toggleTheme}
        title={
          theme === "light" ? "Switch to dark mode" : "Switch to light mode"
        }
      >
        {theme === "light" ? (
          <Moon className="w-5 h-5" />
        ) : (
          <Sun className="w-5 h-5" />
        )}
      </Button>
    </div>
  );
};

export default Sidebar;

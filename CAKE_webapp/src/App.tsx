import { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import Home from "@/components/home";
import ChatPage from "@/pages/ChatPage";
import UploadPage from "@/pages/UploadPage";
import KnowledgePage from "@/pages/KnowledgePage";
import { ThemeProvider } from "@/lib/ThemeProvider";
import { KnowledgeProvider } from "@/lib/KnowledgeProvider";
import { AnimatePresence } from "framer-motion";

function App() {
  return (
    <ThemeProvider>
      <KnowledgeProvider>
        <Suspense fallback={<p>Loading...</p>}>
          <AnimatePresence mode="wait">
            <Routes>
              <Route element={<Layout />}>
                <Route path="/" element={<Home />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/upload" element={<UploadPage />} />
                <Route path="/knowledge" element={<KnowledgePage />} />
              </Route>
            </Routes>
          </AnimatePresence>
        </Suspense>
      </KnowledgeProvider>
    </ThemeProvider>
  );
}

export default App;

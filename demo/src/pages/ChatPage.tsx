import React from "react";
import ChatBox from "@/components/chat/ChatBox";
import KnowledgeBase from "@/components/chat/KnowledgeBase";
import { motion } from "framer-motion";
import { fadeIn, slideUp, pageTransition } from "@/lib/animations";

const ChatPage = () => {
  return (
    <motion.div
      className="h-full p-6 flex flex-col overflow-hidden"
      initial="initial"
      animate="animate"
      exit="exit"
      variants={fadeIn}
      transition={pageTransition}
    >
      <motion.h1 className="text-2xl font-bold mb-6" variants={slideUp}>
        Chat
      </motion.h1>
      <motion.div
        className="flex-1 grid grid-cols-1 md:grid-cols-[1fr_minmax(280px,350px)] gap-6 min-h-0"
        variants={slideUp}
      >
        <ChatBox />
        <KnowledgeBase />
      </motion.div>
    </motion.div>
  );
};

export default ChatPage;

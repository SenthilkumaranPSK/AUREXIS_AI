import { StateCreator } from 'zustand';
import { ChatMessage } from '../types';
import * as api from '@/lib/api';

export interface ChatSlice {
  chatMessages: ChatMessage[];
  currentChatSession: string | null;
  chatLoading: boolean;

  sendMessage: (message: string) => Promise<void>;
  loadChatHistory: (sessionId?: string) => Promise<void>;
  clearChatHistory: () => void;
}

export const createChatSlice: StateCreator<
  ChatSlice & any,
  [["zustand/subscribeWithSelector", never], ["zustand/persist", unknown], ["zustand/immer", never]],
  [],
  ChatSlice
> = (set, get) => ({
  chatMessages: [],
  currentChatSession: null,
  chatLoading: false,

  sendMessage: async (message) => {
    const { currentUser, currentChatSession, isAuthenticated } = get();
    if (!isAuthenticated) return;
    
    set((state) => {
      state.chatLoading = true;
      state.error = null;
    });
    
    try {
      const userMessage: ChatMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      
      set((state) => {
        state.chatMessages.push(userMessage);
      });
      
      const data = await api.sendChatMessage({
        user_id: currentUser?.id,
        message,
        session_id: currentChatSession,
        use_memory: true,
      });
      
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: data.response.content,
        timestamp: data.response.timestamp || new Date().toISOString(),
        confidence: data.response.confidence,
        model: data.response.model,
      };
      
      set((state) => {
        state.chatMessages.push(aiMessage);
        state.chatLoading = false;
      });
    } catch (error) {
      set((state) => {
        state.chatLoading = false;
        state.error = error instanceof Error ? error.message : 'Failed to send message';
      });
    }
  },

  loadChatHistory: async (sessionId) => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getChatHistory(sessionId);
      set((state) => {
        state.chatMessages = data.messages || [];
        state.currentChatSession = sessionId || state.currentChatSession;
      });
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  },

  clearChatHistory: () => {
    set((state) => {
      state.chatMessages = [];
    });
  },
});

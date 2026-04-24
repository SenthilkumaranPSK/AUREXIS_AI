/**
 * Chat Service
 * Handle AI chat operations
 */

import { api } from './api';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatResponse {
  success: boolean;
  response: any;
  session_id: string;
  timestamp: string;
}

export const chatService = {
  /**
   * Send chat message
   */
  sendMessage: async (message: string, sessionId?: string): Promise<ChatResponse> => {
    return api.post<ChatResponse>('/api/chat/message', {
      message,
      session_id: sessionId,
    });
  },

  /**
   * Get chat history
   */
  getChatHistory: async (sessionId: string): Promise<ChatMessage[]> => {
    return api.get<ChatMessage[]>(`/api/chat/sessions/${sessionId}/messages`);
  },

  /**
   * Get chat sessions
   */
  getChatSessions: async (): Promise<ChatSession[]> => {
    return api.get<ChatSession[]>('/api/chat/sessions');
  },

  /**
   * Create new chat session
   */
  createSession: async (title?: string): Promise<ChatSession> => {
    return api.post<ChatSession>('/api/chat/sessions', { title });
  },

  /**
   * Delete chat session
   */
  deleteSession: async (sessionId: string): Promise<void> => {
    return api.delete(`/api/chat/sessions/${sessionId}`);
  },

  /**
   * Get quick actions
   */
  getQuickActions: async (): Promise<string[]> => {
    return api.get<string[]>('/api/chat/quick-actions');
  },
};

export default chatService;

export type CaricatureStyle = 'funny' | 'cartoon' | 'artistic' | 'realistic';

export interface StyleOption {
  id: CaricatureStyle;
  name: string;
  description: string;
  emoji: string;
  prompt: string;
}

export interface CaricatureHistoryItem {
  id: string;
  originalImage: string;
  caricatureImage: string;
  style: CaricatureStyle;
  intensity: number;
  createdAt: string;
}

export interface CaricatureRequest {
  image: string;
  style: CaricatureStyle;
  intensity: number;
}

export interface CaricatureResponse {
  success: boolean;
  image?: string;
  error?: string;
}

export interface AppState {
  originalImage: string | null;
  caricatureImage: string | null;
  selectedStyle: CaricatureStyle;
  intensity: number;
  isGenerating: boolean;
  history: CaricatureHistoryItem[];
}

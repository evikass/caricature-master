import { StyleOption } from '@/types/caricature';

export const STYLE_OPTIONS: StyleOption[] = [
  {
    id: 'funny',
    name: 'Funny',
    description: 'Hilarious exaggerated features',
    emoji: '🤪',
    prompt: 'Create a hilarious exaggerated caricature with comically enlarged facial features, big head, expressive eyes, and funny expressions.',
  },
  {
    id: 'cartoon',
    name: 'Cartoon',
    description: 'Animated character style',
    emoji: '🎨',
    prompt: 'Transform into a vibrant animated cartoon character style with bold outlines, bright colors, simplified shapes.',
  },
  {
    id: 'artistic',
    name: 'Artistic',
    description: 'Hand-drawn illustration style',
    emoji: '🖌️',
    prompt: 'Create an artistic caricature in the style of a hand-drawn illustration with sketch-like quality, artistic brush strokes.',
  },
  {
    id: 'realistic',
    name: 'Realistic',
    description: 'Subtle professional portrait',
    emoji: '✨',
    prompt: 'Create a subtle, refined caricature with gentle exaggeration that enhances unique features while maintaining realistic quality.',
  },
];

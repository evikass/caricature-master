import { NextRequest, NextResponse } from 'next/server';
import ZAI from 'z-ai-web-dev-sdk';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { image, style, intensity } = body;

    if (!image) {
      return NextResponse.json(
        { error: 'Image is required' },
        { status: 400 }
      );
    }

    const zai = await ZAI.create();

    // Style descriptions for caricature
    const styleDescriptions: Record<string, string> = {
      funny: 'hilarious exaggerated caricature, big head small body, comical expression, cartoon style, vibrant colors, humorous distortion',
      cartoon: 'colorful cartoon caricature, animated style, bold outlines, expressive features, Disney-like exaggeration, playful',
      artistic: 'artistic caricature illustration, stylized portrait, creative interpretation, artistic brushstrokes, gallery quality',
      comic: 'comic book style caricature, dynamic pose, bold ink lines, vibrant colors, superhero exaggeration, action-oriented',
      sketch: 'hand-drawn sketch caricature, pencil art style, artistic shading, rough edges, expressive lines, artistic interpretation',
      anime: 'anime manga style caricature, big expressive eyes, stylized features, Japanese animation style, cute exaggeration',
      realistic: 'subtle realistic caricature, slight exaggeration of features, artistic portrait style, professional illustration',
    };

    const selectedStyle = styleDescriptions[style] || styleDescriptions.funny;
    const intensityLevel = intensity || 50;
    
    const prompt = `Create a ${selectedStyle} from this photo. Exaggeration level: ${intensityLevel}%. Focus on the most distinctive facial features while keeping the person recognizable. High quality, detailed, colorful.`;

    // Generate caricature using image-to-image generation
    const response = await zai.images.generations.create({
      prompt: prompt,
      size: '1024x1024',
    });

    const caricatureBase64 = response.data[0]?.base64;

    if (!caricatureBase64) {
      return NextResponse.json(
        { error: 'Failed to generate caricature' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      image: caricatureBase64,
    });

  } catch (error: any) {
    console.error('Caricature generation error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

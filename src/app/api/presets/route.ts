import { NextResponse } from 'next/server';
import { ARMATURE_PRESETS } from '@/lib/armature-generator';

export async function GET() {
  try {
    return NextResponse.json({
      presets: ARMATURE_PRESETS,
    });
  } catch (error) {
    console.error('Error fetching presets:', error);
    return NextResponse.json(
      { error: 'Failed to fetch presets' },
      { status: 500 }
    );
  }
}

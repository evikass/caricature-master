import { NextRequest, NextResponse } from 'next/server';
import { generateBlenderScript, ArmatureSettings } from '@/lib/armature-generator';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate and construct settings
    const settings: ArmatureSettings = {
      height: body.height || 200,
      jointDiameter: body.jointDiameter || 4,
      jointType: body.jointType || 'ball-and-socket',
      fingerCount: body.fingerCount || 4,
      includeEars: body.includeEars || false,
      includeTail: body.includeTail || false,
      printGap: body.printGap || 0.25,
      minWallThickness: body.minWallThickness || 0.8,
    };
    
    // Validate settings
    if (![100, 150, 200, 250, 300].includes(settings.height)) {
      return NextResponse.json(
        { error: 'Invalid height. Must be 100, 150, 200, 250, or 300' },
        { status: 400 }
      );
    }
    
    if (![3, 4, 5, 6].includes(settings.jointDiameter)) {
      return NextResponse.json(
        { error: 'Invalid joint diameter. Must be 3, 4, 5, or 6' },
        { status: 400 }
      );
    }
    
    if (!['ball-and-socket', 'hinge'].includes(settings.jointType)) {
      return NextResponse.json(
        { error: 'Invalid joint type. Must be "ball-and-socket" or "hinge"' },
        { status: 400 }
      );
    }
    
    if (![3, 4, 5].includes(settings.fingerCount)) {
      return NextResponse.json(
        { error: 'Invalid finger count. Must be 3, 4, or 5' },
        { status: 400 }
      );
    }
    
    // Generate the script
    const script = generateBlenderScript(settings);
    
    // Return the script as downloadable content
    return new NextResponse(script, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': `attachment; filename="armature_h${settings.height}mm_j${settings.jointDiameter}mm.py"`,
      },
    });
  } catch (error) {
    console.error('Error generating armature script:', error);
    return NextResponse.json(
      { error: 'Failed to generate armature script' },
      { status: 500 }
    );
  }
}

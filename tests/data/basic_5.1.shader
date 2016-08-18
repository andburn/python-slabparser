Shader "Basic" {
Properties {
 _MainTex ("Main Texture", 2D) = "white" { }
 _LightingBlend ("Ambient Lighting Blend", Float) = 0
}
SubShader {
 Tags { "RenderType"="Opaque" "Highlight"="true" }
 Pass {
  Tags { "RenderType"="Opaque" "Highlight"="true" }
  Fog {
   Color (0,0,0,0)
  }
  GpuProgramID 13277
Program "vp" {
SubProgram "d3d9 " {
Bind "vertex" Vertex
Float 0 [_LightingBlend]
"vs_2_0
def c0, 1, 0, 0, 0
mov oD0, c0.x

"
}
}
Program "fp" {
SubProgram "d3d9 " {
SetTexture 0 [_MainTex] 2D 0
"ps_2_0
def c0, 1, 1, 0, 0
texld r0, c0.xy, s0
mov oC0, r0

"
}
}
 }
}
Fallback "Diffuse"
}

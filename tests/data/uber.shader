Shader "Uber" {
Properties {
 _MainTex ("Portrait (RGB)", 2D) = "black" { }
 _Color_Light ("FX1 Color", Color) = (1,1,1,1)
 _Vividness ("Vividness", Float) = 1
 _Layer1_Position ("Layer1 Rotation Position", Range(-0.5,0.5)) = 0.5
}
SubShader {
 Tags { "RenderType"="Opaque" "Highlight"="true" }
 Pass {
  Name "MADUBER"
  Tags { "RenderType"="Opaque" "Highlight"="true" }
  Fog {
   Color (0,0,0,1)
  }
  GpuProgramID 8497
Program "vp" {
SubProgram "d3d9 " {
Keywords { "LOW_QUALITY" "LYR3_COMBINE" "LYR3_SINGLE" }
Bind "vertex" Vertex
Bind "texcoord" TexCoord0
Bind "texcoord1" TexCoord1
Matrix 0 [glstate_matrix_mvp]
Float 1 [_LightingBlend]
"vs_3_0
def c0, 2, -1, 1, -3
dcl_something1 v0.xy
dp4 t0.x, c0, v0
mad t0.xy, v0, c0, c0.zwzw

"
}
SubProgram "d3d9 " {
Keywords { "LYR4_COMBINE" }
Bind "vertex" Vertex
Bind "texcoord" TexCoord0
Bind "texcoord1" TexCoord1
Matrix 0 [glstate_matrix_mvp]
Float 1 [_LightingBlend]
"vs_3_0
def c0, 2, -1, 1, -3
dcl_something1 v0.xy
dp4 t0.x, c0, v0
mad t0.xy, v0, c0, c0.zwzw

"
}
}
Program "fp" {
SubProgram "d3d9 " {
Keywords { "LOW_QUALITY" "LYR3_COMBINE" "LYR3_SINGLE" }
SetTexture 0 [_MainTex] 2D 0
"ps_3_0
def c0, 0.130000321, 0, 0, 0
dcl_texcoord v0.xy
dcl_color_pp v2
dcl_2d s0
texld_pp r0, v0, s0
mov oC0, r0
"
}
SubProgram "d3d9 " {
Keywords { "LYR4" "BLENDALPHA_L3" }
Vector 23 [_Distortion]
Vector 0 [_Color]
Float 22 [_Intensity]
SetTexture 0 [_MainTex] 2D 0
SetTexture 1 [_ShadowTex] 2D 1
"ps_3_0
def c41, 0.7, -0.5, 0.5, 0.115800047
dcl_texcoord v0.xy
dcl_texcoord1 v1.xy
dcl_texcoord2 v2
dcl_color_pp v6.xyz
dcl_2d s0
dcl_2d s1
texld r0, v2, s4
mov r1.x, c24.x
mov_pp oC0.w, c24.x

"
}
}
 }
}
Fallback "Diffuse"
}

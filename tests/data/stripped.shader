Shader "Stripped" {
Properties {
 _Color ("Color", Color) = (1,1,1,1)
 _Rotation ("Rotation", Vector) = (1,1,0,0)
}
SubShader {
 Tags { "RenderType"="Opaque" "Highlight"="true" }
 Pass {
  Name "SUBER"
  Tags { "RenderType"="Opaque" "Highlight"="true" }
  GpuProgramID 4477
Program "vp" {
SubProgram "d3d9 " {
GpuProgramIndex 0
}
SubProgram "d3d9 " {
GpuProgramIndex 1
}
SubProgram "d3d9 " {
GpuProgramIndex 2
}
}
Program "fp" {
SubProgram "d3d9 " {
GpuProgramIndex 4
}
SubProgram "d3d9 " {
GpuProgramIndex 5
}
SubProgram "d3d9 " {
GpuProgramIndex 6
}
}
 }
}
Fallback "Diffuse"
}

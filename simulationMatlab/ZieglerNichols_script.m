clear
clc
close all

G_num = [5];
G_den = [ 1 6 11 6 ];

KU = 60;
TU = 1.9;

%Use the custom Z-N
[KP, KI,KD] = ZieglerNichols (KU, TU ,'NoOvershoot')
%[KP, KI,KD] = ZieglerNichols (KU, TU ,'SomeOvershoot')
%ch?n lu?t trong d?u ''
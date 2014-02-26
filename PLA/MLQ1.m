f = load('./trainningset.dat');
flag = 0;
f1 = f(:,1:4);
f2 = f(:,5);
[m,n] = size(f1);
n = zeros(m);
n = n + 1;
n = n(:,1);
combination = [n,f1];
w = [0,0,0,0,0];
final = PLA(w,combination,f2)   


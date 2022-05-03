omega_a = 10.5;
omega_b = 10;
r = 0.1;
D = 0.2;
L = 2.5;
R = [0,-1;1,0];
v = 0.5857;

dT = 0.1;
T = 100;
N = ceil(T/dT);

x = zeros(2,N);
h = x;
h(:,1) = [cos(v);sin(v)];

x_b = x;
h_b = x;

x_b(:,1) = x(:,1) - L * h(:,1);
h_b(:,1) = h(:,1);



for i = 1 : N-1;
    
    %robot
    omega_s = r*(omega_a + omega_b)/2;
    dot_x = h(:,i) *omega_s;
    x(:,i+1) = x(:,i) + dT * dot_x;
    omega_m = r*(omega_a-omega_b)/D;
    
    dot_h = R*h(:,i)*omega_m;
    h(:,i+1) = h(:,i) + dT * dot_h;
    h(:,i+1) =h(:,i+1)/norm(h(:,i+1));
    
    %bed
    dot_x_b = omega_s * h_b(:,i) * (h(:,i)' * h_b(:,i));
    dot_h_b = omega_s * ((h(:,i)-h_b(:,i)*(h(:,i)' * h_b(:,i)))/L);
    x_b(:,i+1) = x_b(:,i) + dT * dot_x_b;
    h_b(:,i+1) = h_b(:,i) + dT * dot_h_b;
    h_b(:,i+1) =h_b(:,i+1)/norm(h_b(:,i+1));
    
    clf
    plot(x(1,i),x(2,i),'g*',x_b(1,i),x_b(2,i),'r*')
    hold on
    plot([x(1,i) x_b(1,i)], [x(2,i) x_b(2,i)])
    hold off
    axis([-10 10 -10 10]);
    pause(0.2);
end

%% 
x_r(0) = x(1,0)
x_r(T) = x(1,T)
dot_x_r(0) = dot_x %= h(1,0) * omega_s = h(1,0) r*(omega_a + omega_b)/2
dot_x_r(T) = dot_x %= h(1,T) * omega_s = h(1,T) r*(omega_a + omega_b)/2

h_r(0) = h(1,0)
h_r(T) = h(1,T)

x_r(t)=a*t^3 + b*t^2 + c*t + d
dot_x = 3*a*t^2 + 2*b*t + c
dot_dot_x = 6*a*t + 2*b

x(1,0) = d
dot_x(1,0) = c
x(1,T) = d + c*T + b*T^2 + a*T^3
dot_x(1,T) = c + 2*b*T + 3*a*T^2
%%
tf = 2

x_r_0 = [1;0]
x_r_T = [2;1]
v = 90
v1 = 0
h_r_0 = [cos(deg2rad(v));sin(deg2rad(v))]
h_r_T = [cos(deg2rad(v1));sin(deg2rad(v1))]

d = x_r_0(1)
c = h_r_0(1)
b = (3/(tf^2)) * (x_r_T(1) - x_r_0(1)) - 1/tf * (2*h_r_0(1) + h_r_T(1))
a = - 2/(tf^3) * (x_r_T(1) - x_r_0(1)) + 1/(tf^2) * (h_r_0(1) + h_r_T(1))

d1 = x_r_0(2)
c1 = h_r_0(2)
b1 = (3/(tf^2)) * (x_r_T(2) - x_r_0(2)) - 1/tf * (2*h_r_0(2) + h_r_T(2))
a1 = - 2/(tf^3) * (x_r_T(2) - x_r_0(2)) + 1/(tf^2) * (h_r_0(2) + h_r_T(2))

T = 0:0.05:tf


x_r=a*T.^3 + b*T.^2 + c*T + d
hold on
y_r=a1*T.^3 + b1*T.^2 + c1*T + d1


plot (x_r,y_r)
hold on
%plot (x_r)
%plot (y_r)


syms t omega r real
x = [a*t^3 + b*t^2 + c*t + d, a1*t^3 + b1*t^2 + c1*t + d1]
dx=jacobian(x,t)
ws=norm(dx)
simplify(ws)
%ws = (abs(t/2 + 0)^2 + abs(t/2-1)^2^(1/2))

omegaS = (abs(T/2 + 0).^2 + abs(T/2-1).^2.^(1/2))

mean(omegaS)

point1 = [x_r(10); y_r(10)]
point2 = [x_r(20); y_r(20)]
point3 = [x_r(30); y_r(30)]


vector1 = point2-point1
vector2 = point3-point2

dh = vector2-vector1
dh = dh / norm(dh)
R = [0,-1;1,0];


w_m = dot(dh,R*vector1/norm(vector1))

plot (point1(1),point1(2), '.', 'markersize', 8)
plot (point2(1),point2(2),'.', 'markersize',8)
plot (point3(1),point3(2),'.', 'markersize',8)

hold off

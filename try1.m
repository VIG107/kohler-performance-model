clc
Temp_Data = readtable("Water_Data.xlsx");
Temp_Data.Properties.VariableNames{'Var1'} = 'T_in';
Temp_Data.Properties.VariableNames{'Var2'} = 'rho';
Temp_Data.Properties.VariableNames{'Var3'} = 'neta';
Temp_Data.Properties.VariableNames{'Var4'} = 'k';

T_in = input('Enter Hot Water Inlet Temperature in °C: ');
T_room = input('Enter Ambient Temperature (°C): ');
L = input('Enter the Length of Hose(mm): ')/1000;
vol_flow_rate = input('Enter the volume flow rate in lpm: ');
vol_flow_rate2 = vol_flow_rate * 0.0000167; % convert lpm to m3/s
disp(Temp_Data.Properties.VariableNames);

c_p = 4180;

r1 = 4.5/2000; % inner radius
r3 = 11/2000; % outer radius
r2 = 9.5/2000; % outer radius of EPDM Pipe

k_EPDM = 0.25;
k_vinyl = 0.2;

h_out = 500;
area = pi * (r1)^2;

index = Temp_Data.T_in == T_in;

if any(index)
    rho = Temp_Data.rho(index);
    neta = Temp_Data.neta(index);
    k = Temp_Data.k(index);
    disp('Selected row values:');
    disp(Temp_Data(index, :));
else
    rho = 1000;
    neta = 0.000547;
    k = 0.6;
end

mfr = rho * vol_flow_rate2; % volume to mass flow rate

V = vol_flow_rate2 / area; % velocity

Re = (rho * V * 2*r1) / (neta); % Reynolds number

Pr = (c_p * neta) / k;

if Re < 4000
    h_in = (3.66 * k) / (2*r1); % Convective Heat Transfer Coefficient at inlet
else
    h_in = (0.023 * Re^0.8 * Pr^0.4 * k) / (2*r1);
end

Q_unit_length = (2 * pi * (T_in - T_room)) / ((1 / (h_in * r1)) + (log(r2/r1) / k_EPDM) + (log(r3/r2) / k_vinyl) + (1 / (h_out * r3)));
Q_total = Q_unit_length * L; % Total Heat Loss

delta_T = Q_total / (mfr * c_p) + 0.2537;
T_out = T_in - delta_T; % Outlet Temperature

fprintf('Velocity of water: %.3f m/s\n', V);
fprintf('Heat Loss Per Unit Length: %.3f W\n', Q_unit_length);
fprintf('Total Heat Loss: %.3f W\n', Q_total);
fprintf('Approximate Temperature Drop: %.3f °C\n', delta_T);
fprintf('Expected Outlet Temperature from Hose: %.3f °C\n', T_out);
[signalStruct] = ReadMSEEDFast('CHUS_titanSMA_2137_20240818_091000.seed'); %archivo seed

Z_comp=signalStruct(1).data;
N_comp=signalStruct(2).data;
E_comp=signalStruct(3).data;

FC=2; % cuentas/micro g - Sensitivity
Z_comp_corr=Z_comp*(1/(FC/0.00098066));
N_comp_corr=N_comp*(1/(FC/0.00098066));
E_comp_corr=E_comp*(1/(FC/0.00098066));

%%corregir Z
z_mean=mean(Z_comp_corr);
z=Z_comp_corr-z_mean;


figure(100)
plot(CHUS180820240410Ecorr(1,1),CHUS180820240410Ecorr(1:8001,2),'k');
xlabel('time (s)');
ylabel('acc (cm/s^2)');
legend('E-W')
grid on

figure(101)
plot(CHUS180820240410Ncorr(1:8001,1),CHUS180820240410Ncorr(1:8001,2),'k');
xlabel('time (s)');
ylabel('acc (cm/s^2)');
legend('N-S')
grid on

figure(102)
plot(CHUS180820240410Zcorr(1:8001,1),CHUS180820240410Zcorr(1:8001,2),'k');
xlabel('time (s)');
ylabel('acc (cm/s^2)');
legend('Z')
grid on

figure(103)
plot(CHUS080720240454Ecorr(:,2),CHUS080720240454Ncorr(:,2),'k');
xlabel('acc E-W (cm/s^2)');
ylabel('acc N-S (cm/s^2)');
legend('E-W')
grid on

figure(104)
plot(sa_E(:,1),sa_E(:,2),'r'); hold on
plot(sa_N(:,1),sa_N(:,2),'b');
plot(sa_Z(:,1),sa_Z(:,2),'k');
xlabel('T (s)');
ylabel('SA (cm/s^2)');
legend('E-W','N-S','Z')
grid on

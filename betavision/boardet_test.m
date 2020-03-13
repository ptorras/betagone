%%%%%%% Deteccio de tauler i peces %%%%%%%
clearvars
clc
close all

% Carregar fitxer qualsevol

filepath = fullfile('.', 'testpic', 'P_20200306_184440_vHDR_On.jpg');
im_test = double(rgb2gray(imread(filepath)));

dimension = size(im_test);

im_test = im_test( floor(dimension(1) * 0.24) : floor(dimension(1) * 0.76) ...
    , floor(dimension(2) * 0.05) : floor(dimension(2) * 0.99));

figure();
imshow(im_test, []);

% Binaritzacio de la imatge

im_test = double(im_test > graythresh(im_test)*255)*255;

% Aplicar deteccio de vores
vores = edge(im_test, 'Canny');
[H, theta, rho] = hough(vores);     % H -> Matriu Hough
                                    % theta -> Angles emprats
                                    % rho -> valors rho assolits

pics = houghpeaks(H, 30);
n_pics = numel(pics(:,1));

linies = houghlines(vores, theta, rho, pics);

figure();

subplot(1,3,1);
imshow(im_test, []);

subplot(1,3,2);
imshow(vores, []);

subplot(1,3,3);
imshow(im_test, []);

hold on;

for i=1:length(linies)
   xy = [linies(i).point1; linies(i).point2];
   plot(xy(:,1), xy(:,2), 'LineWidth', 3, 'Color', 'blue');
   hold on;
end

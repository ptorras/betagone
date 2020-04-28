clearvars
clc
close all

taulell = imread("./testpic/taulell.png");

nf3 = imread("./testpic/nf3.png");
sicilian = imread("./testpic/sicilian.png");
starting = imread("./testpic/starting.png");
ze4 = imread("./testpic/ze4.png");

% figure, imshow(nf3);
% figure, imshow(sicilian);
% figure, imshow(starting);
% figure, imshow(ze4);

taulell = taulell(:,428:1495,:);



red = taulell(:,:,1);
green = taulell(:,:,2);

red = wiener2(red,[10 10]);

red = red >= graythresh(red)*255;
green = green >= graythresh(green)*255;

kernel = strel("square", 100);


red = not(imclose(not(red), kernel));
green = not(imclose(not(green), kernel));


% figure, imshow(red,[]);
% figure, imshow(green,[]);
figure, imshow(taulell .* uint8(repmat(red,1,1,3)));
figure, imshow(taulell .* uint8(repmat(green,1,1,3)));
% se = strel("square", 3);
% red_dilated = imerose(red, se);
%figure, imshow(uint8(red-red_dilated),[]);
%figure, imshow(uint8(green-green_dilated),[]);

dimension = size(red);

vores = edge(red, 'Canny');
[H, theta, rho] = hough(vores);     % H -> Matriu Hough
                                    % theta -> Angles emprats
                                    % rho -> valors rho assolits

pics = houghpeaks(H, 18);
n_pics = numel(pics(:,1));

linies = houghlines(vores, theta, rho, pics, 'FillGap', max(dimension), 'MinLength', 100);

figure();

imshow(ze4, []);

hold on;

for i=1:length(linies)
   xy = [linies(i).point1; linies(i).point2];
   plot(xy(:,1)+428, xy(:,2), 'LineWidth', 3, 'Color', 'yellow');
   hold on;
end

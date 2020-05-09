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

%taulell = taulell(:,428:1495,:);

red = taulell(:,:,1);
green = taulell(:,:,2);


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

res = print_lines(red, green, ze4);
% res = rgb2gray(res);
% res = res(:,:) > 70;
% se = strel('square',10);
% res = imdilate(res,se);
% figure, imshow(res);
% 
% print_lines2(res, ze4);

function res = print_lines(red, green, ze4)

    linies_red = make_lines(red);
    linies_green = make_lines(green);
    
    img_black = zeros(size(ze4));
    
    figure();
    imshow(img_black);

    hold on;
    
     for i=1:length(linies_red)
        xy_red = [linies_red(i).point1; linies_red(i).point2];
        xy_green = [linies_green(i).point1; linies_green(i).point2];
        plot(xy_red(:,1), xy_red(:,2), 'LineWidth', 10, 'Color', 'yellow');
        plot(xy_green(:,1), xy_green(:,2), 'LineWidth', 10, 'Color', 'magenta');
        hold on;
     end
     
     hold off;
     h = findobj(gca,'Type','line');
     x=get(h, 'Xdata');
     y=get(h, 'Ydata');
     x = cell2mat(x);
     y = cell2mat(y);
     disp(x);
     disp(y);
     F = getframe();
     res = F.cdata;

end

% function print_lines2(im_test, ze4)
%     linies = make_lines(im_test);
% 
%     figure();
%     imshow(ze4);
%     
%     hold on;
% 
%     for i=1:length(linies)
%        xy = [linies(i).point1; linies(i).point2];
%        plot(xy(:,1), xy(:,2), 'LineWidth', 3, 'Color', 'red');
%        hold on;
%     end
%     
% end

function linies = make_lines(img)

    dimension = size(img);

    vores = edge(img, 'Canny');
    [H, theta, rho] = hough(vores);     % H -> Matriu Hough
                                        % theta -> Angles emprats
                                        % rho -> valors rho assolits

    pics = houghpeaks(H, 18);
    %n_pics = numel(pics(:,1));

    linies = houghlines(vores, theta, rho, pics, 'FillGap', max(dimension), 'MinLength', 100);
    
end

function crossings = detect_intersections(img)

end
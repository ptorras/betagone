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

crop_board(red, green, ze4);
% res = rgb2gray(res);
% res = res(:,:) > 70;
% se = strel('square',10);
% res = imdilate(res,se);
% figure, imshow(res);
% 
% print_lines2(res, ze4);

function crop_board(red, green, ze4)

    linies_red = make_lines(red);
    linies_green = make_lines(green);
    
    % COORDINATES OF BOARD
    x0g = [linies_green(:).point1];
    x0g = reshape(x0g,2,numel(x0g)/2)';
    x0r = [linies_red(:).point1];
    x0r = reshape(x0r,2,numel(x0r)/2)';
    
    % T = top, B = bottom, R = RIGHT, L = LEFT, C = CORNER
    [tlc,~] = min(x0r);
    [brc,~] = max(x0g);
    trc = [brc(1),tlc(2)];
    h = [tlc(1),tlc(2);trc(1),trc(2)];
    d = pdist(h,'euclidean');
    step = (d/8);
    
    %img_black = zeros(size(ze4));
    
    
    %figure(), imshow(ze4);

    %hold on;
    
%      for i=1:length(linies_red)
%         xy_red = [linies_red(i).point1; linies_red(i).point2];
%         xy_green = [linies_green(i).point1; linies_green(i).point2];
%         plot(xy_red(:,1), xy_red(:,2), 'LineWidth', 3, 'Color', 'yellow');
%         plot(xy_green(:,1), xy_green(:,2), 'LineWidth', 3, 'Color', 'magenta');
%         hold on;
%      end

     %F = getframe();
     %res = F.cdata;
     
     % t_img = taulell separat amb imatges.
     
     t_img = cell(8,8);
     
     for i =0:7
         
        y1 = tlc(2) + i*step;
        y2 = y1 + step;
        
        
        for j =0:7
            
            x1 = tlc(1) + j*step;
            x2 = x1 + step; 
            
            casella = imcrop(ze4, [x1 y1 x2-x1 y2-y1]);
            
            t_img{i+1,j+1} = imresize(casella, [133, 133]);
            
            subplot(8,8,(i*8)+(j+1));
            im_gray = rgb2gray(t_img{i+1,j+1}); %I'M GRAY
            level = graythresh(im_gray);
            BW = imbinarize(im_gray,level); imshow(BW);
            simpleColorDetection
            %im_edge = edge(im_gray, 'Canny'); imshow(im_edge);
            
        end     
     end
     
    figure(), imshow(ze4);
    
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
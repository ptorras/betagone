clc;    % Clear the command window.
close all;  % Close all figures (except those of imtool.)
clear;  % Erase all existing variables. Or clearvars if you want.
workspace;  % Make sure the workspace panel is showing.
format long g;
format compact;
fontSize = 15;
%===============================================================================
% Get the name of the image the user wants to use.
baseFileName = 'taulell.png'; % Assign the one on the button that they clicked on.
% Get the full filename, with path prepended.
folder = 'testpic'; % Determine where demo folder is (works with all versions).
fullFileName = fullfile(folder, baseFileName);
%===============================================================================
% Read in a demo image.
grayImage = imread(fullFileName);
% Get the dimensions of the image.
% numberOfColorChannels should be = 1 for a gray scale image, and 3 for an RGB color image.
[rows, columns, numberOfColorChannels] = size(grayImage);
if numberOfColorChannels > 1
  % It's not really gray scale like we expected - it's color.
  % Use weighted sum of ALL channels to create a gray scale image.
  grayImage = rgb2gray(grayImage);
  % ALTERNATE METHOD: Convert it to gray scale by taking only the green channel,
  % which in a typical snapshot will be the least noisy channel.
  % grayImage = grayImage(:, :, 2); % Take green channel.
end
% Display the image.
figure;
imshow(grayImage, []);
axis on;
caption = sprintf('Original Gray Scale Image');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
drawnow;
hp = impixelinfo();
% Set up figure properties:
% Enlarge figure to full screen.
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
% Get rid of tool bar and pulldown menus that are along top of figure.
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
% Give a name to the title bar.
set(gcf, 'Name', 'Demo by ImageAnalyst', 'NumberTitle', 'Off')
hold on;
drawnow;
checkerBoardRows = round(linspace(14, 1268, 9));
checkerBoardColumns = round(linspace(11, 1257, 9));
for row = 1 : length(checkerBoardRows)
  thisRow = checkerBoardRows(row);
  line([thisRow, thisRow], [checkerBoardRows(1), checkerBoardRows(end)],...
    'Color', 'r', 'LineWidth', 2);
end
for col = 1 : length(checkerBoardColumns)
  thisCol = checkerBoardColumns(col);
  line([checkerBoardColumns(1), checkerBoardColumns(end)], [thisCol, thisCol],...
    'Color', 'r', 'LineWidth', 2);
end
figure;
plotNumber = 1;
% Now crop out 64 chunks.
for row = 1 : length(checkerBoardRows)-1
  row1 = checkerBoardRows(row);
  row2 = checkerBoardRows(row+1) - 1;
  for col = 1 : length(checkerBoardColumns)-1
    col1 = checkerBoardColumns(col);
    col2 = checkerBoardColumns(col+1) - 1;
    subplot(8, 8, plotNumber);
    subImage = grayImage(row1:row2, col1:col2);
    imshow(subImage);
    drawnow;
    if plotNumber == 1
      % Set up figure properties:
      % Enlarge figure to full screen.
      set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
      % Get rid of tool bar and pulldown menus that are along top of figure.
      set(gcf, 'Toolbar', 'none', 'Menu', 'none');
      % Give a name to the title bar.
      set(gcf, 'Name', 'Demo by ImageAnalyst', 'NumberTitle', 'Off')
      hold on;
      drawnow;      
    end
    plotNumber = plotNumber + 1;
  end
end
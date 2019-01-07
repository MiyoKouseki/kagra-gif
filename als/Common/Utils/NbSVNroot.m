function [ path ] = NbSVNroot
%NBSVNROOT Returns the root of the NbSVN directory tree containing this function

path = [fileparts(fileparts(fileparts(mfilename('fullpath')))) filesep];

end


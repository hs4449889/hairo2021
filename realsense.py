from numpy.lib.type_check import real
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2

class REALSENSE:
    def __init__(self, frame_size, frame_rate):
        # set_frame
        self.frame_size = frame_size
        self.frame_rate = frame_rate

        # Configre
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Get device product line for setting a supporting resolution
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                self.found_rgb = True
                break
        if not self.found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, self.frame_size[0], self.frame_size[1], rs.format.z16, self.frame_rate)
        self.config.enable_stream(rs.stream.color, self.frame_size[0], self.frame_size[1], rs.format.bgr8, self.frame_rate)

        # start_streaming
        self.pipeline.start(self.config)

    def On_Mouse(self, event, _x, _y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.depth = self.depth_frame.get_distance(_x, _y)
            self.x = _x
            self.y = _y

    def Get_Frame(self):
        try:
            # Wait for a coherent pair of frames: depth and color
            self.frames = self.pipeline.wait_for_frames()
            self.depth_frame = self.frames.get_depth_frame()
            self.color_frame = self.frames.get_color_frame()
            self.depth = 0
            if not self.depth_frame or not self.color_frame:
                1/0

            # Convert images to numpy arrays
            self.depth_image = np.asanyarray(self.depth_frame.get_data())
            self.color_image = np.asanyarray(self.color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)

            self.depth_colormap_dim = self.depth_colormap.shape
            self.color_colormap_dim = self.color_image.shape

            # If depth and color resolutions are different, resize color image to match depth image for display
            if self.depth_colormap_dim != self.color_colormap_dim:
                self.resized_color_image = cv2.resize(self.color_image, dsize=(self.depth_colormap_dim[1], self.depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                self.images = np.hstack((self.resized_color_image, self.depth_colormap))
            else:
                self.images = np.hstack((self.color_image, self.depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', self.images)
            cv2.setMouseCallback('RealSense', self.On_Mouse)
            cv2.waitKey(1)
        except ZeroDivisionError:
            pass

realsense = REALSENSE([640, 480], 15)

while True:
    try:
        realsense.Get_Frame()
        if realsense.depth != 0:
            print("RealSense_Depth  >>>  X: {:3d}, Y: {:3d}, D: {:5.1f}".format(realsense.x, realsense.y, realsense.depth*100))
    except KeyboardInterrupt:
        realsense.pipeline.stop()
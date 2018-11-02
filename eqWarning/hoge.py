import matplotlib.pyplot as plt
from obspy.taup import TauPyModel
import numpy as np

model = TauPyModel(model="iasp91")


arrivals = model.get_ray_paths(source_depth_in_km=500,
                               distance_in_degree=120,
                               phase_list=['ttbasic'])
                               #phase_list=["Pdiff", "Sdiff",
                               #"pPdiff", "sSdiff"])
# 
fig = plt.figure(figsize=(12,12))
ax1 = fig.add_subplot(221,polar=True)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(224)
ax4 = fig.add_subplot(223)
ax2.invert_yaxis()
ax4.invert_yaxis()

# calc incident angle 
ray = arrivals[0]
dist = np.rad2deg(ray.path["dist"])
depth = ray.path["depth"]
_dx = (dist[-2] - dist[-1])
_dy = (depth[-2] - depth[-1])
_dr = np.sqrt(_dx**2+_dy**2)
dr = depth[0]
dx = _dx*dr/_dr
dy = _dy*dr/_dr
print('Incident Angle is {0:3.1f}'.format(np.rad2deg(np.arctan2(dy,dx))))

# plot
ax1 = arrivals.plot_rays(fig=fig,ax=ax1)
ax2 = arrivals.plot_rays(plot_type='cartesian',fig=fig,ax=ax2)
ax3 = arrivals.plot_times(ax=ax3)
ax4.plot(dist,depth,label=ray.name)
ax4.arrow(x=dist[-1]+dx,y=depth[-1]+dy,dx=-dx,dy=-dy,width=1,head_width=2,head_length=dr/10,length_includes_head=True,color='k')
         
#
ax3.legend(loc='lower right')
ax4.legend(loc='lower right')
plt.savefig('hoge.png')
plt.close()


#つぎは実際の地震について計算する。
#レイリー波についても入射方向を求めるようにする。

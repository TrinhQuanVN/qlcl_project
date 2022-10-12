import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates

import random
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.text as text
import matplotlib.collections as collections

import matplotlib.cbook as cbook

from basic_units import cm, inch

def a():
    rng = np.arange(50)
    rnd = np.random.randint(1,10,size=(3,rng.size))
    yrs = rng + 1950
    print(rnd)
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.stackplot(yrs,rnd + rnd, labels=['Eas','Eur','Oce'])
    ax.set_title('Combined')
    ax.legend(loc = 'upper left')
    ax.set_ylabel('Total')
    ax.set_xlim(xmin=yrs[0],xmax=yrs[-1])
    fig.tight_layout()


    plt.show()
    
def b():
    x = [datetime.date.today() + datetime.timedelta(days=i) for i in range(10)]
    print(x)
    y = np.random.randint(0,50,size=(len(x)))
    print(y)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(x[0],x[-1])
    ax.set_xticks()
    
    ax.set_ylim(min(y),max(y))
    ax.plot(x,y)
    plt.show()
    
def c():
    x = np.random.randint(1,11,50)
    y = x + np.random.randint(1,5,x.size)
    print(x)
    print(y)
    data = np.column_stack((x,y))
    print(data)
    fig, (ax1,ax2) = plt.subplots(1,2,figsize = (8,4))
    
    ax1.scatter(x,y,marker='o',c='r') #,edgecolors='b'
    ax1.set_title('Scatter')
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
    
    # ax2.hist(data,bins=np.arange(data.min(),data.max()),label=('x','y'))
    ax2.hist(data,label=('x','y'))
    
    ax2.set_title('frequence of $x$ and $y$')
    ax2.legend(loc=(0.8, 0.8))
    ax2.yaxis.tick_right()
    plt.show()
    
def d():
    start = '2021-01-01'
    end = '2021-09-01'
    work_id = [f'W{i}' for i in range(100)]
    ngay = np.arange(start=start,stop=end,dtype='M8')
    nhan_cong_theo_ngay = np.random.randint(5,200,ngay.size)
    
    fig,(ax1,ax2) = plt.subplots(2,1,figsize=(16,8))
    
    ax1.set_xticks(ngay)
    ax1.set_yticklabels(work_id)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(r'%d/%m'))
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter(r'%d/%m'))
    
    
    line = lines.Line2D([ ngay[0],ax1.yaxis.get_major_ticks], [ngay[2],'W0'],
                        lw=2, color='black', axes=ax1)   
    
    ax1.add_line(line)

    
    ax2.bar(ngay,nhan_cong_theo_ngay,width=2,linewidth=0.7)
    # for i in range(ngay.size):
    #     ax2.text(ngay[i],nhan_cong_theo_ngay[i],nhan_cong_theo_ngay[i])
    # ax2.text(ngay,nhan_cong_theo_ngay,nhan_cong_theo_ngay)
    # ax2.axis(option='tight')
    ax2.set_xticks(ngay)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter(r'%d/%m'))
    ax2.xaxis.set_minor_formatter(mdates.DateFormatter(r'%d/%m'))
    # ax2.set_xlim(ngay[0],ngay[-1])
    # ax2.xaxis.
    
    # line = lines.Line2D([ngay[0],ngay[1]], [10,20],
    #                     lw=2, color='black', axes=ax1)   
     
    # ax2.add_line(line)
    
    plt.xticks(rotation=90)   
    
    fig.tight_layout()
    plt.show()
    
    
def e():
    fig, ax = plt.subplots()
    ax.xaxis.set_units(cm)
    ax.yaxis.set_units(cm)

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    if 0:
        # test a line collection
        # Not supported at present.
        verts = []
        for i in range(10):
            # a random line segment in inches
            verts.append(zip(*inch*10*np.random.rand(2, random.randint(2, 15))))
        lc = collections.LineCollection(verts, axes=ax)
        ax.add_collection(lc)

    # test a plain-ol-line
    line = lines.Line2D([0*cm, 1.5*cm], [0*cm, 2.5*cm],
                        lw=2, color='black', axes=ax)
    ax.add_line(line)

    if 0:
        # test a patch
        # Not supported at present.
        rect = patches.Rectangle((1*cm, 1*cm), width=5*cm, height=2*cm,
                                alpha=0.2, axes=ax)
        ax.add_patch(rect)


    t = text.Text(3*cm, 2.5*cm, 'text label', ha='left', va='bottom', axes=ax)
    ax.add_artist(t)
    


    ax.set_xlim(-1*cm, 10*cm)
    ax.set_ylim(-1*cm, 10*cm)
    # ax.xaxis.set_units(inch)
    ax.grid(True)
    ax.set_title("Artists with units")
    plt.show()
    
    
def f():


    # Load a numpy record array from yahoo csv data with fields date, open, high,
    # low, close, volume, adj_close from the mpl-data/sample_data directory. The
    # record array stores the date as an np.datetime64 with a day unit ('D') in
    # the date column.
    data = cbook.get_sample_data('goog.npz', np_load=True)['price_data']

    fig, axs = plt.subplots(3, 1, figsize=(6.4, 7), constrained_layout=True)
    # common to all three:
    for ax in axs:
        ax.plot('date', 'adj_close', data=data)
        # Major ticks every half year, minor ticks every month,
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.grid(True)
        ax.set_ylabel(r'Price [\$]')

    # different formats:
    ax = axs[0]
    ax.set_title('DefaultFormatter', loc='left', y=0.85, x=0.02, fontsize='medium')

    ax = axs[1]
    ax.set_title('ConciseFormatter', loc='left', y=0.85, x=0.02, fontsize='medium')
    ax.xaxis.set_major_formatter(
    mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

    ax = axs[2]
    ax.set_title('Manual DateFormatter', loc='left', y=0.85, x=0.02,
                fontsize='medium')
    # Text in the x axis will be displayed in 'YYYY-mm' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    plt.show()
    
    
if __name__ =="__main__":
    f()
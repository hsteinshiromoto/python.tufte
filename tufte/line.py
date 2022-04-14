def line(x, y, df=None, figsize=(16, 8), linestyle='tufte', linewidth=1.0, color='black', alpha=0.9, ticklabelsize=10, markersize=10, **kwargs):
    x, y = check_df(x, y, df)
    fig, ax = plt.subplots(figsize=figsize)
    plot_style(ax, plot_type='line')
    if linestyle == 'tufte':
        if len(kwargs) > 0:
            warnings.warn('Marker options are being ignored')
        marker = 'o'
        ax.plot(x, y, linestyle='-', linewidth=linewidth, color=color, alpha=alpha, zorder=1)
        ax.scatter(x, y, marker=marker, s=markersize*8, color='white', zorder=2)
        ax.scatter(x, y, marker=marker, s=markersize, color=color, zorder=3)
    else:
        ax.plot(x, y, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha, markersize=markersize ** 0.5, **kwargs)
    ax = range_frame(ticklabelsize, ax, x, y, dimension='both')
    return fig, ax
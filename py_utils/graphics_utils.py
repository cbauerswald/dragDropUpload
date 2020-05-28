import matplotlib.pyplot as plt
import re
import os

'''
From Graphics Utils:
'''

FIG_EXTENSION = 'png'


def section_topics_barplot_gen(section_df, TEST_NAME, student, section_name, dpath):

    box = section_df.groupby(['topic', 'correct']).size().unstack(fill_value=0)

    ax = box.plot.bar(stacked=True, yticks=[])
    xticklabels = ax.get_xticklabels()
    ax.set_xticklabels(xticklabels, rotation=45, ha="right")

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 0:
            ax.text(x + width / 2,
                    y + height / 2,
                    f'{int(height)}',
                    horizontalalignment='center',
                    verticalalignment='center')
    plt.legend(['Incorrect', 'Correct'], prop={'size': 10})

    plt.title(f'{student} - {section_name.title()} Topics')

    x_axis = ax.axes.get_xaxis()
    x_label = x_axis.get_label()
    x_label.set_visible(False)

    plt.tight_layout()

    fig = ax.get_figure()

    img_fname = re.sub(r'\s', '-', f'{student}-{section_name}-topics-fig.{FIG_EXTENSION}')
    save_path = os.path.join(dpath, img_fname)
    fig.savefig(save_path)
    plt.close()

    '''
    AWS URL for Topics Fig:
    '''
    base = 'https://ibidnyc.s3.amazonaws.com/tests'
    url_fpath = re.sub(r'\s', '+', f'{TEST_NAME}/{student}/{section_name}/{img_fname}')
    final_url = os.path.join(base, url_fpath)

    return final_url

def section_subtopics_barplot_gen(ans_w_bkdn, TEST_NAME, student, section_name, dpath):
    topic_groups = ans_w_bkdn.groupby(['topic', 'subtopic', 'correct']).size().unstack(fill_value=0)
    img_paths = []
    for topic in ans_w_bkdn.topic.unique():
        ax = topic_groups.loc[topic, :, :].droplevel(0).plot.bar(stacked=True)
        xticklabels = ax.get_xticklabels()
        ax.set_xticklabels(xticklabels, rotation=45, ha="right")

        for p in ax.patches:
            width, height = p.get_width(), p.get_height()
            if height > 0:
                x, y = p.get_xy()
                ax.text(x + width / 2,
                        y + height / 2,
                        f'{int(height)}',
                        horizontalalignment='center',
                        verticalalignment='center')

        plt.legend(['Incorrect', 'Correct'], prop={'size': 10})
        plt.title(f'{student} - {section_name.title()} Subtopic: {topic.title()}')


        x_axis = ax.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)

        plt.tight_layout()

        fig = ax.get_figure()
        img_fname = re.sub(r' ', '-', f'{student}-{section_name}-subtopic-{topic}-fig.{FIG_EXTENSION}')

        '''
        AWS URL for Sub-Topics Fig:
        '''
        base = 'https://ibidnyc.s3.amazonaws.com/tests'
        url_fpath = re.sub(r'\s', '+', f'{TEST_NAME}/{student}/{section_name}/subsections/{img_fname}')
        final_url = os.path.join(base, url_fpath)

        save_path = os.path.join(dpath, img_fname)

        img_paths.append(final_url)
        fig.savefig(save_path)
        plt.close()

    return img_paths
from commands.PUBG.border_chop import corp_margin
from skimage import io
import dataframe_image as dfi
import os

def export_image(df, df_name, my_name, time_path, font_size = 2):
  image_name = str(my_name) + '_stat_' + df_name + '_' + time_path + '.png'
  
  df_styled = df.style.hide_index()

  df_styled = df.style.set_table_styles([
      {'selector': 'td', 'props': [('background-color', '#2F3136'), ('color', 'white'), ('font-size', '{}em'.format(font_size))]},
      {'selector': 'th:not(.index_name)', 'props': 'background-color: #202225; color: white; font-size : {}em;'.format(font_size)}, 
      {'selector': '', 'props': 'border: 1px solid #2F3136'}
      ], overwrite=False)  
  
  dfi.export(df_styled, image_name)
  print('{} complete.'.format(df_name))

  im = io.imread(image_name)
  img_re = corp_margin(im)
  image_name_re = my_name + '_stat_' + df_name + '_re_' + time_path + '.png'
  io.imsave(image_name_re,img_re)
  print('{}_re complete'.format(df_name))
  os.remove(image_name)
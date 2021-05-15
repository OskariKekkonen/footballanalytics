#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:38:31 2021

@author: oskari.kekkonen
"""

import pandas as pd
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt

# .csv -tiedoston luku
df = pd.read_csv('InterAway.csv')

# onnistuneiden syöttöjen erittely
passes = df[df['Event']=='Pass']
successful = passes[passes['Outcome']=='Successful']

# lukuarvojen muuttaminen desimaaleiksi (float -arvoiksi)
pas = pd.to_numeric(successful['Passer'],downcast='integer')
rec = pd.to_numeric(successful['Recipient'],downcast='integer')
successful['Passer'] = pas
successful['Recipient'] = rec

# syöttöjen keskimääräiset sijainnit ja lukumäärä
average_locations = successful.groupby('Passer').agg({'X':['mean'],'Y':['mean','count']})
average_locations.columns = ['X','Y','count']


# pelaajien välisten keskenäisten syöttöjen tunnistus
pass_between = successful.groupby(['Passer','Recipient']).id.count().reset_index()
pass_between.rename({'id':'pass_count'},axis='columns',inplace=True)

# yhdistetään datakehykset
pass_between = pass_between.merge(average_locations, left_on='Passer',right_index=True)
pass_between = pass_between.merge(average_locations, left_on='Recipient',right_index=True,suffixes=['', '_end'])

# minimi lukumäärä kombinaatioille
pass_between = pass_between[pass_between['pass_count']>3]


# kentän piirto, käytetään juego de posicion -mallia

pitch = pitch = Pitch(positional=True, shade_middle=True, positional_color='#eadddd', shade_color='#f2f2f2')
fig, ax = pitch.draw()


# nuolien piirto

arrows = pitch.arrows(1.2*pass_between.X,.8*pass_between.Y,1.2*pass_between.X_end,.8*pass_between.Y_end,
                     width = 2, headwidth = 3.5, color = 'black', ax = ax, zorder = 1, alpha = .5)

# pisteiden piirto

nodes = pitch.scatter(1.2*average_locations.X,.8*average_locations.Y,
                     s = 200, color = 'y', edgecolors = "black", linewidth = 1, alpha = 1, zorder = 1, ax=ax)

# pelaajien numerot pisteisiin
for index, row in average_locations.iterrows():
     pitch.annotate(row.name, xy=(1.2*row.X,0.8*row.Y), c='black', va='center', ha='center', size=9, fontweight='bold',ax=ax)

# taustavärin määrittely
fig.patch.set_facecolor('w')

# otsikon ja kommenttien lisäys 
ax.set_title("KuPS vs Inter Turku (vieras) 24/04 ", fontsize=12, color="black", fontfamily="Andale Mono", fontweight='bold', pad=-8)

pitch.annotate("twitter: @oskarikekkonen", (57, 84), color='black',
               fontsize=10, ha='center', va='center', ax=ax, fontweight='bold', fontfamily="Andale Mono")

#save the plot
plt.savefig('Inter-KuPS.png', dpi = 500, bbox_inches='tight',facecolor='w')

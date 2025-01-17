# import stuff

import pandas as pd
import sys
import numpy as np

# set display to max
pd.set_option('display.max_column', None)

def get_full_length_data():
    '''
    merges segment data into full length data
    :return:
    '''
    infile = 'abdb_outfiles_2019/respairs_segment_notationx_len_merged_angle.csv'
    df = pd.read_csv(infile)
    # exclude segment with no paratope
    df = df.dropna(subset=['paratope'])
    segments_dict = {'L': ['LFR1', 'CDR-L1', 'LFR2', 'CDR-L2', 'LFR3', 'CDR-L3', 'LFR4'],
                     'H': ['HFR1', 'CDR-H1', 'HFR2', 'CDR-H2', 'HFR3', 'CDR-H3', 'HFR4']}
    data = []
    for pdbid in df.pdbid.unique():
        pdbdf = df[df.pdbid == pdbid]
        chains = pdbdf.abchain.unique()
        for chain in chains:
            chaindf = pdbdf[pdbdf.abchain == chain]
            segments = segments_dict[chain]
            paratopes = []
            abresnumisets = []
            ab_motiflens = []
            ab_motifs = []
            gapstrstats = []
            # print(chaindf)
            for segment in segments:
                try:
                    segdf = chaindf[chaindf.segment == segment]
                    paratope = segdf.paratope.tolist()
                    paratopes += paratope
                    abresnumisets += segdf.abresnumiset.tolist()
                    ab_motiflens += segdf.ab_motiflen.tolist()
                    ab_motifs += segdf.ab_motif.tolist()
                    gapstrstats += segdf.gapstrstatus.tolist()
                except:
                    print('not in list')
            print(paratopes,abresnumisets, pdbid)
            chain_paratope = ''.join(paratopes)
            chain_abresnumiset = '-'.join(abresnumisets)
            chain_motiflen = sum(ab_motiflens)
            chain_motif = ''.join(ab_motifs)
            gapstrstatus = sorted(set(gapstrstats))[-1]
            motif_per_chain = len(ab_motifs)
            datum = [pdbid, chain, chain_paratope, chain_abresnumiset, chain_motif, chain_motiflen, gapstrstatus, motif_per_chain]
            data.append(datum)
    colnames = ['pdbid', 'abchain', 'paratope', 'abresnumiset', 'ab_motif', 'ab_motiflen', 'gapstrstatus',
                'motif_per_chain']
    outdf = pd.DataFrame(data, columns=colnames)
    outname = infile.split('len')[0] + '_full_length.csv'
    outdf.to_csv(outname, index=False)


def get_region_lengths():
    '''
    get region lengths for each complex
    :return:
    '''
    infile = 'abdb_outfiles_2019/respairs_segment_notationx_len_merged_angle_bnaber_phil_pc.csv'
    df = pd.read_csv(infile)
    print(df.head())
    segment_str_path = '/Users/rahmadakbar/greifflab/aims/aimugen/datasets/segment_structures'
    region_lens = []
    for i,row in df.iterrows():
        # print(row)
        pdbid = row.pdbid
        chain = row.abchain
        segment = row.segment
        filename = '%s_%s_%s.pdb' % (pdbid, chain, segment)
        filepath = segment_str_path + '/' + filename
        contents = open(filepath).read().splitlines()
        resnumis = []
        for content in contents:
            resnum = content[22:26].strip()
            insertion = content[27]
            resnumi = resnum + insertion
            resnumis.append(resnumi)
        region_len = len(set(resnumis))
        region_lens.append(region_len)
    print(len(region_lens))
    df['region_len'] = region_lens
    print(df.head())
    outfile = infile.split('.')[0] + '_reglen.csv'
    print(outfile)
    df.to_csv(outfile, index=False)






# run stuff
# get_full_length_data()
get_region_lengths()











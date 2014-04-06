
from workshops.lib import coll
from workshops.lib.features import get_dfs

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	dfs_sorted = sorted(get_dfs(coll_data).items(), key=lambda t: (-t[1], t[0]))
	print('{:<50}{:}'.format('TERM', 'DOC_FREQ'))
	for term, freqs in dfs_sorted:
		print('{:<50}{:}'.format(term, freqs))

if __name__ == '__main__':
	main()

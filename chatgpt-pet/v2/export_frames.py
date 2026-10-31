"""Export the validated atlas into transparent PNG frames for desktop integration."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

STATES = [('idle',6),('running-right',8),('running-left',8),('waving',4),('jumping',5),('failed',8),('waiting',6),('running',6),('review',6)]
ANGLES = ['000','022.5','045','067.5','090','112.5','135','157.5','180','202.5','225','247.5','270','292.5','315','337.5']

def main():
    base=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    atlas_path=base/'Suey-v2.png'
    manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(atlas_path.read_bytes()).hexdigest()
    if digest != manifest['atlas_sha256']:
        raise SystemExit('Atlas hash differs from the validated bundle.')
    with Image.open(atlas_path) as source:
        if source.size != (1536,2288) or source.mode != 'RGBA':
            raise SystemExit('Expected the 1536x2288 RGBA v2 atlas.')
        jobs=[(state,index,row,index) for row,(state,count) in enumerate(STATES) for index in range(count)]
        jobs += [('look',angle,9+i//8,i%8) for i,angle in enumerate(ANGLES)]
        for state,index,row,col in jobs:
            destination=args.output/state/f'{index:02}.png' if isinstance(index,int) else args.output/state/f'{index}.png'
            destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.exists():
                raise SystemExit(f'Refusing to overwrite {destination}; choose an empty output directory.')
        for state,index,row,col in jobs:
            destination=args.output/state/f'{index:02}.png' if isinstance(index,int) else args.output/state/f'{index}.png'
            source.crop((col*192,row*208,(col+1)*192,(row+1)*208)).save(destination)
    print(f'Exported {len(jobs)} frames to {args.output}')

if __name__=='__main__':
    main()

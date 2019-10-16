from dataquality.dataquality import DataQuality
with DataQuality('./dataquality/dqflag.db') as db:
    total      = db.ask('select startgps,endgps from EXV_SEIS')
    available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
    lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2')
    lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4')
    glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')
    use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                        'and startgps>={0} and endgps<={1}'.format(args.start,args.end))

bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)
if bad!=0:
    raise ValueError('SegmentList Error: Missmatch the number of segments.')    

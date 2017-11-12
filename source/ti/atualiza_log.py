#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys

def atualizaLog(log, imageLog):
    
    
    logLines = []
    imageLogLines = imageLog.readlines()
    
    for log in log.readlines():
        log = log.strip().split(';')
        logLines.append(log)

    for line in imageLogLines:
        line = line.strip().split(';')
        if len(line) == 2:
            fileName = line[0]
            valorAEEJ = line[1]
            
            for log in logLines:
                if len(log) == 15:
                    if log[14] == fileName:
                        log[9] = valorAEEJ
                        break

    for i in range(0,len(logLines)):
        logLines[i] = ';'.join(logLines[i])

    return '\n'.join(logLines) + '\n'
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--log','-l', type=argparse.FileType('r'), help='Arquivo de log gerado pela biblioteca avalgame', required=True)
    parser.add_argument('--imageLog','-i', type=argparse.FileType('r'), help='Arquivo de log gerado pela pela rede neural', required=True)
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help='Arquivo de log atualizado')
    args = parser.parse_args()
    
    newLog = atualizaLog(args.log, args.imageLog)

    args.output.write(newLog)


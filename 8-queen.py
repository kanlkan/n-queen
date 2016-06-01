#! /usr/bin/env python
# encoding=utf-8

# 8 Queens Problem

import sys
import random

gGeneCnt = 4
gMutationSpan = 4
gRange = 0
gVec = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
gGaIdx = [4, 6]

def makeIniGene():
	ini_gene = []
	for cnt in range(0,gGeneCnt):
		line = []
		for i in range(0, 8):
			val = random.randint(0, 7)
			line.append(val)

		ini_gene.append(line)

	return ini_gene

def calcFitness(gene):
	fitness = 0
	board = []
	line = []
	for i in range(0, 8):
		line = []
		for j in range(0, 8):
			if j == gene[i]:
				line.append(1)
			else:
				line.append(0)
		board.append(line)

	for i in range(0, 8):
		for j in range(0, 8):
			val = getCell(board, (i,j), (0,0))
			if val == 1:
				for vec in gVec:
					for k in range(1, 8):
						valofst = getCell(board, (i,j), (vec[0]*k, vec[1]*k))
						if valofst == 1:
							fitness += 1
						elif valofst == -1:
							break

	return fitness

def getCell(board, pos, ofst):
	posx = pos[0] + ofst[0]
	posy = pos[1] + ofst[1]
	if posx >= 0 and posy >= 0 and posx < 8 and posy < 8:
		val = board[posx][posy]
	else:
		val = -1
	
	return val

def simpleGa(gene_list, rank_list):
	new_gene_list = []
	for i in range(0, gGeneCnt):
		if i == rank_list[3]:
			new_gene_list.append(gene_list[rank_list[0]])
		else:
			new_gene_list.append(gene_list[i])

	updated_gene_list = []
	line1 = []
	line2 = []
	for i in range(0, 8):
		if i < gGaIdx[0]:
			line1.append(new_gene_list[rank_list[0]][i])
			line2.append(new_gene_list[rank_list[1]][i])
		else:
			line1.append(new_gene_list[rank_list[1]][i])
			line2.append(new_gene_list[rank_list[0]][i])
	updated_gene_list.append(line1)
	updated_gene_list.append(line2)
	
	line1 = []
	line2 = []
	for i in range(0, 8):
		if i < gGaIdx[1]:
			line1.append(new_gene_list[rank_list[2]][i])
			line2.append(new_gene_list[rank_list[3]][i])
		else:
			line1.append(new_gene_list[rank_list[3]][i])
			line2.append(new_gene_list[rank_list[2]][i])
	updated_gene_list.append(line1)
	updated_gene_list.append(line2)
	
	return updated_gene_list

def printBoard(gene):
	for i in range(0, len(gene)):
		line = []
		for j in range(0, len(gene)):
			if j == gene[i]:
				line.append(1)
			else:
				line.append(0)

		print line

def main(argv):
	gene_list = makeIniGene()
	print "Initial gene = " + str(gene_list)

	fitness = []
	for i in range(0, gGeneCnt):
		fitness.append(0)

	loop = 0
	while True :
		loop += 1
		idx = 0
		max_fitness_idx = []
		min_fitness_idx = []

		# mutation
		if loop % gMutationSpan == 0:
			geneidx = random.randint(0, gGeneCnt-1)
			posidx = random.randint(0,  7)
			valrand = random.randint(0,  7)
			gene_list[geneidx][posidx] = valrand

		# compare fitness
		for gene in gene_list:
			fitness[idx] = calcFitness(gene)
			if idx == 0:
				max_fitness_idx = (fitness[0], 0)
				min_fitness_idx = (fitness[0], 0)

			if max_fitness_idx[0] < fitness[idx]:
				max_fitness_idx = (fitness[idx], idx)

			if min_fitness_idx[0] > fitness[idx]:
				min_fitness_idx = (fitness[idx], idx)

			print fitness[idx]
			idx += 1

		min_fitness = min(fitness)
		if min_fitness <= gRange:
			print "Loop end = " + str(loop) + ", Fitness = " +  str(min_fitness)
			printBoard(gene_list[min_fitness_idx[1]])
			break

		ranktemp = []
		for i in range(0, gGeneCnt):
			if i !=  max_fitness_idx[1] and i != min_fitness_idx[1]:
				ranktemp.append(i)

		if fitness[ranktemp[0]] > fitness[ranktemp[1]]:
			rank_list = [ min_fitness_idx[1], ranktemp[1], ranktemp[0], max_fitness_idx[1] ]
		else:
			rank_list = [ min_fitness_idx[1], ranktemp[0], ranktemp[1], max_fitness_idx[1] ]

		updated_gene_list = []
		updated_gene_list = simpleGa(gene_list, rank_list)
		gene_list = updated_gene_list


if __name__ == "__main__":
        main(sys.argv)

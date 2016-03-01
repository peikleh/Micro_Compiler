keywords = ('EQ_EQ',
			'PLUS',
			'MINUS',
			'MULT',
			'DIV',
			'EQ',
			'N_EQ',
			'LESS',
			'MORE',
			'L_PAR',
			'R_PAR',
			'R_PAR',
			'L_EQ',
			'R_EQ')

for i in keywords:
	print ("T_" + i + " = (r\"" + i +"\")")
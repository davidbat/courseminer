import math

def auc(x,y):
	s = 0.0 

	for i in range(1, len(x)):
		s += (x[i] - x[i-1]) * (y[i] + y[i-1])
	return s / 2.0

def bayes_mod(db, means):
	bern_db = []
	if len(db) == 0:
		return []
	num_features = len(db[0]) - 1
	num_taken = sum(map(lambda val:val[-1], db))
	num_ntaken = len(db) - num_taken
	alph = 1.0 / num_features
	d = num_features
	# for every feature`
	# ignore the first feature cause its the student id
	for i in range(len(db[0]) - 1):
		inner = []
		p_less_taken = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 1)), db).count(1) + alph) / (num_taken + alph * d)
		p_more_taken = 1 - p_less_taken
		p_less_ntaken = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 0)), db).count(1) + alph) / (num_ntaken + alph * d)
		p_more_ntaken = 1 - p_less_ntaken
		inner = [p_less_taken, p_more_taken, p_less_ntaken, p_more_ntaken]
		bern_db.append(inner)
	return bern_db

def predict_bayes(model, means, data_point, prior):
	if model == []:
		return prior
	taken = math.log(prior, 2)
	ntaken = math.log((1 - prior), 2)
	for i in range(len(data_point) - 1):
		if data_point[i] <= means[i]:
			taken += math.log(model[i][0], 2)
			ntaken += math.log(model[i][2], 2)
		else:
			taken += math.log(model[i][1], 2)
			ntaken += math.log(model[i][3], 2)
	return 1.0 if taken > ntaken else 0.0
	#return math.exp(taken)
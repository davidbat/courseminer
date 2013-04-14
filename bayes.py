import math

def auc(x,y):
	s = 0.0 

	for i in range(1, len(x)):
		#print x[i] - x[i-1],y[i] + y[i-1]
		s += (x[i] - x[i-1]) * (y[i] + y[i-1])
	return s / 2.0

def bayes_mod(db, means):
	bern_db = []
	#for each in db:
	# bern_db.append(map(lambda val, mean:int(val > mean) , each, attributes))
	# for every feature
	if len(db) == 0:
		return []
	num_features = len(db[0]) - 1
	num_spam = sum(map(lambda val:val[-1], db))
	num_nspam = len(db) - num_spam
	alph = 1.0 / num_features
	d = num_features
	# for every feature
	# ignore the first feature cause its the student id
	for i in range(len(db[0]) - 1):
		inner = []
		p_less_spam = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 1)), db).count(1) + alph) / (num_spam + alph * d)
		p_more_spam = 1 - p_less_spam
		#p_more_spam = float(map(lambda val:int((val[i] > means[i]) & (val[-1] == 1)), db).count(1) + alph) / (num_spam + alph * d)
		p_less_nspm = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 0)), db).count(1) + alph) / (num_nspam + alph * d)
		p_more_nspm = 1 - p_less_nspm
		#p_more_nspm = (map(lambda val:int((val[i] > means[i]) & (val[-1] == 0)), db).count(1) + alph) / (num_nspam + alph * d)
		inner = [p_less_spam, p_more_spam, p_less_nspm, p_more_nspm]
		#if p_less_spam ==0 or p_more_spam ==0 or p_less_nspm == 0 or p_more_nspm == 0 or p_less_spam+p_more_spam <= .99 or p_less_spam+p_more_spam >= 1.01:
		#  print inner
		#print inner
		bern_db.append(inner)
	#print bern_db
	return bern_db

def predict_bayes(model, means, data_point, prior):
	if model == []:
		return prior
	spam = math.log(prior, 2)
	nspam = math.log((1 - prior), 2)
	for i in range(len(data_point) - 1):
		if data_point[i] <= means[i]:
			spam += math.log(model[i][0], 2)
			nspam += math.log(model[i][2], 2)
		else:
			spam += math.log(model[i][1], 2)
			nspam += math.log(model[i][3], 2)
	return 1.0 if spam > nspam else 0.0
	
	#return math.exp(spam)
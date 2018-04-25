import csv
import json

csvfile = open('Trend_hashtag.csv', 'r')
jsonfile = open('Trend_hashtag.json', 'w')

fieldnames = ("id","ht_name","ts_start","t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18", "t19", "t20", "t21", "t22", "t23", "t24", "t25", "t26", "t27", "t28", "t29", "t30", "t31", "t32", "t33", "t34", "t35", "t36", "t37", "t38", "t39", "t40", "t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50", "t51", "t52", "t53", "t54", "t55", "t56", "t57", "t58", "t59", "t60", "t61", "t62", "t63", "t64", "t65", "t66", "t67", "t68", "t69", "t70", "t71", "t72", "t73", "t74", "t75", "t76", "t77", "t78", "t79", "t80", "t81", "t82", "t83", "t84", "t85", "t86", "t87", "t88", "t89", "t90", "t91", "isTrend", "predict", "lrs", "dtc", "gpc", "knc", "mlp", "lsv", "pac", "bnb", "bkn", "gnb", "ncc", "rfc", "tca", "etc", "rlm", "lpc", "gbc", "rcf")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
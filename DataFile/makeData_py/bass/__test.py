import Rule

a = Rule.RuleComposite()
b = Rule.RuleComposite()
c = Rule.RuleComposite()
d = Rule.RuleComposite()

a.append(b)
a.append(c)
c.append(d)

print(a)
print(b)
print(c)
print(d)


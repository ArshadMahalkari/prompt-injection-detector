import random

def mutate_text(text):
    mutations = [
        lambda t: t.replace("ignore", "ign0re"),
        lambda t: t.replace("instructions", "instr."),
        lambda t: t.replace("you are", "ur"),
        lambda t: t.replace("system", "sys"),
    ]

    mutation = random.choice(mutations)
    return mutation(text)


def generate_attack(text):
    for _ in range(random.randint(1, 3)):
        text = mutate_text(text)
    return text
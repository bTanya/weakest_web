from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import BattleField


def form(env):
    cl = int(env.get('CONTENT_LENGTH', '0'))
    d = env['wsgi.input'].read(cl).decode(encoding='utf-8')
    d = parse_qs(d)

    soldiers = int(d.get('soldiers')[0])
    vehicles = int(d.get('vehicles')[0])
    squads_number_ = int(d.get('squads_number')[0])
    armies_number_ = int(d.get('armies_number')[0])
    strategy_ = str(d.get('strategy')[0])[2:-1]

    with open('result.html', 'r') as f:
        if 5 <= soldiers + vehicles <= 10 and squads_number_ >= 2 and \
                        armies_number_ >= 2:
            battle = BattleField.BattleField(armies_number=armies_number_,
                                             strategy=strategy_,
                                             squads_number=squads_number_,
                                             soldiers_number=soldiers,
                                             vehicles_number=vehicles)
            win = 'Won the army: ' + str(battle.start())
            res = [(f.read() % (win,)).encode('UTF-8')]
        else:
            err = 'ERR: Input wrong number.'
            res = [(f.read() % (err,)).encode('UTF-8')]
    return res


route = {
    'form': form
}


def app(env, resp_start):
    resp_start('200 OK', [('Content-Type', 'text/html')])

    path = env.get('PATH_INFO', '/')[1:]
    parts = path.split('/')

    res = ''
    if len(parts) > 0 and parts[0]:
        fn = route.get(parts[0])
        if fn is not None:
            res = fn(env)
    else:
        with open('index.html', 'r') as f:
            res = [f.read().encode('UTF-8')]
    return res


if __name__ == "__main__":
    serv = make_server('', 8080, app)
    serv.serve_forever()
    serv.shutdown()

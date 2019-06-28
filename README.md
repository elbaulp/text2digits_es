# text2digits_es

Convert a variety text numbers into its numerical representation in Spanish

## Examples

```python
assert '99 PORCENTAJE' == text2num('99%')
assert '9' == text2num('nueve')
assert '2013' == text2num('dos mil trece')
assert 'tengo 2 caballos' == text2num('tengo dos caballos')
assert 'tengo 2000 casas' == text2num('tengo dos mil casas')
assert 'unas 2405 propiedades' == text2num('unas dos mil cuatrocientas cinco propiedades')
assert 'tengo 1800 vinos' == text2num('tengo mil ochocientos vinos')
assert '1200000 cosas y 3 casas' == text2num('Un millón doscientas mil cosas y tres casas')
assert '125000 cosas y 3 casas' == text2num('ciento veinticinco mil cosas y tres casas')
assert '124.3 decimetros, tambien tengo' == text2num('ciento veinticuatro con treinta decimetros, tambien tengo')
assert 'ghjghjg hj con fecha 26 DE JUNIO DEL AÑO 2013 en Granada' == text2num('ghjghjg hj con fecha VEINTISÉIS DE JUNIO DEL AÑO DOS MIL TRECE en Granada')
assert 'para responder de 1.250.000 euros de principal; intereses ordinarios durante' == text2num('para responder de 1.250.000 euros de principal; intereses ordinarios durante')
assert 'de 31.224,16 Euros y demas' == text2num('de 31.224,16 Euros y demas')
assert 'con fecha 22 de Diciembre de 2010' == text2num('con fecha veintidós de Diciembre de dos mil diez')
assert '30003' == text2num('tres hectareas y tres centiareas')
assert 'de 205871.01 EUROS de' == text2num('de DOSCIENTOS CINCO MIL OCHOCIENTOS SETENTA Y UN EUROS CON UN CENTIMO de')
```

## Contrubute

All contributions all welcome!, fell free to make pull requests.
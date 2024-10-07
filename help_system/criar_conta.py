from flask import render_template, redirect, url_for, flash, request
from help_system import app
from help_system.forms import FormCriarConta
from help_system.models import Usuario


@app.route('/criar-conta', methods=['GET', 'POST'])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=form_criarconta.senha.data
        )
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criar_conta.html', form_criarconta=form_criarconta)

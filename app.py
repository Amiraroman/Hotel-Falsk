from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from Entity import Base, Habitacion, Reserva, Cliente

app = Flask(__name__)
app.secret_key = '123456'

# Configurar la conexión a la base de datos

engine = create_engine('postgresql://postgres:00000000@localhost/HOTEL')
Base.metadata.bind = engine

# Crear una sesión de base de datos
DBSession = sessionmaker(bind=engine)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/habitacion')
def listar_habitacion():
    session = DBSession()
    habitaciones = session.query(Habitacion).all()
    session.close()
    return render_template('habitacion.html', habitaciones=habitaciones)

@app.route('/habitacion/agregar', methods=['GET', 'POST'])
def agregar_habitacion():
    if request.method == 'POST':
        session = DBSession()
        try:
            nueva_habitacion = Habitacion(
                numero_habitacion=request.form['numero_habitacion'],
                tipo_habitacion=request.form['tipo_habitacion'],
                precio=request.form.get('precio')
            )
            session.add(nueva_habitacion)
            session.commit()
            flash('Habitación agregada exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al agregar la habitación. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_habitacion'))
    else:
        return render_template('agregar_habitacion.html')

@app.route('/habitacion/editar/<int:id_habitacion>', methods=['GET', 'POST'])
def editar_habitacion(id_habitacion):
    session = DBSession()
    habitacion = session.query(Habitacion).filter_by(idhabitacion=id_habitacion).first()

    if request.method == 'POST':
        try:
            habitacion.numero_habitacion = request.form['numero_habitacion']
            habitacion.tipo_habitacion = request.form['tipo_habitacion']
            habitacion.precio = request.form.get('precio')
            session.commit()
            flash('Habitación editada exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al editar la habitación. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_habitacion'))
    else:
        session.close()
        return render_template('editar_habitacion.html', habitacion=habitacion)

@app.route('/habitacion/eliminar/<int:id_habitacion>', methods=['GET', 'POST'])
def eliminar_habitacion(id_habitacion):
    session = DBSession()
    try:
        habitacion = session.query(Habitacion).filter_by(idhabitacion=id_habitacion).first()
        if habitacion:
            session.delete(habitacion)
            session.commit()
            flash('Habitación eliminada exitosamente!', 'success')
        else:
            flash('Habitación no encontrada.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar la habitación.', 'danger')
    finally:
        session.close()
    return redirect(url_for('listar_habitacion'))


@app.route('/cliente')
def listar_cliente():
    session = DBSession()
    clientes = session.query(Cliente).all()
    session.close()
    return render_template('cliente.html', clientes=clientes)


@app.route('/cliente/agregar', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        session = DBSession()
        try:
            nuevo_cliente = Cliente(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                direccion=request.form['direccion'],
                num_pasaporte=request.form.get('num_pasaporte')
            )
            session.add(nuevo_cliente)
            session.commit()
            flash('Cliente agregado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al agregar el cliente. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_cliente'))
    else:
        return render_template('agregar_cliente.html')



@app.route('/cliente/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    session = DBSession()
    cliente = session.query(Cliente).filter_by(idcliente=id_cliente).first()

    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.apellido = request.form['apellido']
            cliente.direccion = request.form['direccion']
            cliente.num_pasaporte = request.form.get('num_pasaporte')
            session.commit()
            flash('Cliente editado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al editar el cliente. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_cliente'))
    else:
        session.close()
        return render_template('editar_cliente.html', cliente=cliente)

@app.route('/cliente/eliminar/<int:id_cliente>', methods=['GET', 'POST'])
def eliminar_cliente(id_cliente):
    session = DBSession()
    try:
        cliente = session.query(Cliente).filter_by(idcliente=id_cliente).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            flash('Cliente eliminado exitosamente!', 'success')
        else:
            flash('Cliente no encontrado.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar el cliente.', 'danger')
    finally:
        session.close()
    return redirect(url_for('listar_cliente'))




if __name__ == '__main__':
    app.run(debug=True)

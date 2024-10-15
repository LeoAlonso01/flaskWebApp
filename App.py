from flask import Flask, flash, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
import boto3
import os
from werkzeug.utils import secure_filename
# Initialize Flask
app = Flask(__name__)

# aws configuration
S3_BUCKET = "arn:aws:s3:::myawsbucket13102024"
S3_KEY = "AKIAZPPF7WVWMCB4JADV"
S3_SECRET = "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"
S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"

# Configurations
s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

# Configuración de subida de archivos permitidos
app.config["UPLOAD_FOLDER"] = "/tmp"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

# Función para verificar si la extensión del archivo es válida
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Secret key for session
app.secret_key = 'my_secret_key'

# MySQL Connection
app.config['MYSQL_HOST'] = 'bc7592clo3zzpn1yahhq-mysql.services.clever-cloud.com' # 'localhost'
app.config['MYSQL_USER'] =  'uhnkoggbedux6dqh' # 'root'
app.config['MYSQL_PASSWORD'] = 'XplC0tzNalRAbzgcccm0'
app.config['MYSQL_DB'] = 'bc7592clo3zzpn1yahhq' #'flask_mysql' 


# Initialize MySQL
mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# upload images to s3
@app.route('/upload_file', methods=['POST'])
def upload_file_to_s3():
    print(request.files)
    return jsonify({'message': 'File uploaded successfully'})

# Products
@app.route('/products', methods=['GET'])
def products():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    if (len(products) == 0):        
        return jsonify({'message': 'No products found'})
    print(products)
    return render_template('products.html', products=products)  

# Add Product
@app.route('/add_product', methods=['POST'])
def add_product():
    
    # Verifica si la solicitud es un POST
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quiantity = request.form['quiantity']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO products (name, price, quiantity) VALUES (%s, %s, %s)', (name, price, quiantity))
        mysql.connection.commit()
        cursor.close()
        flash('Producto agregado exitosamente')
        return redirect(url_for('index'))
    
# Details
@app.route('/details/<string:id>', methods=['GET'])
def details(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE id = {0}'.format(id))
    product = cursor.fetchone()
    cursor.close()
    if product:
        return render_template('details.html', product=product)
    else:
        flash
        return redirect(url_for('index'))

# Edit
@app.route('/edit/<string:id>')
def edit_prodct(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE id = {0}'.format(id))
    product = cursor.fetchone()
    return render_template('edit.html', product=product)

# Update
@app.route('/update/<string:id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quiantity = request.form['quiantity']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE products SET name = %s, price = %s, quiantity = %s WHERE id = %s', (name, price, quiantity, id))
        mysql.connection.commit()
        cursor.close()
        flash('Product updated successfully')
        return redirect(url_for('index'))
    
# Delete
@app.route('/delete/<string:id>')
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM products WHERE id = {0}'.format(id))
    cursor.connection.commit()
    cursor.close()
    flash('Product removed successfully')
    return redirect(url_for('index'))
    # return f" el producto que sera eliminado sera el  {id}"

if __name__ == '__main__':
    app.run(port=3000, debug=True)



#!/usr/bin/env python3
"""
Script para crear las tablas necesarias en la base de datos
"""

import sys
from sqlalchemy import create_engine, text
from app.core.config.settings import settings

def create_tables():
    """Crear las tablas necesarias en la base de datos"""
    print("🚀 Creating database tables...")
    
    try:
        # Conectar a la base de datos
        engine = create_engine(settings.database_url)
        
        # SQL para crear la tabla evaluations
        create_evaluations_sql = """
        CREATE TABLE IF NOT EXISTS evaluations (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            estimated_level VARCHAR(10) NOT NULL,
            grammar FLOAT NOT NULL,
            vocabulary FLOAT NOT NULL,
            fluency FLOAT NOT NULL,
            mistakes TEXT NOT NULL,
            suggestions TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # SQL para crear índices
        create_indexes_sql = """
        CREATE INDEX IF NOT EXISTS idx_evaluations_user_id ON evaluations(user_id);
        CREATE INDEX IF NOT EXISTS idx_evaluations_level ON evaluations(estimated_level);
        CREATE INDEX IF NOT EXISTS idx_evaluations_created_at ON evaluations(created_at);
        """
        
        # Ejecutar las consultas
        with engine.connect() as conn:
            # Crear tabla
            conn.execute(text(create_evaluations_sql))
            print("✅ Table 'evaluations' created successfully")
            
            # Crear índices
            conn.execute(text(create_indexes_sql))
            print("✅ Indexes created successfully")
            
            # Confirmar cambios
            conn.commit()
            
            # Verificar que las tablas existen
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('questions', 'evaluations')
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"✅ Tables in database: {tables}")
            
            # Mostrar estructura de la tabla evaluations
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'evaluations'
                ORDER BY ordinal_position;
            """))
            
            print("\n📋 Structure of 'evaluations' table:")
            for row in result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"  - {row[0]}: {row[1]} ({nullable})")
        
        print("\n🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def verify_tables():
    """Verificar que todas las tablas necesarias existen"""
    print("\n🔍 Verifying database tables...")
    
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as conn:
            # Verificar tabla questions
            result = conn.execute(text("SELECT COUNT(*) FROM questions"))
            questions_count = result.scalar()
            print(f"✅ Questions table: {questions_count} records")
            
            # Verificar tabla evaluations
            result = conn.execute(text("SELECT COUNT(*) FROM evaluations"))
            evaluations_count = result.scalar()
            print(f"✅ Evaluations table: {evaluations_count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Database Migration Script")
    print("=" * 50)
    
    # Crear tablas
    if create_tables():
        # Verificar tablas
        verify_tables()
        print("\n✅ Migration completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Run: python test_endpoints.py")
        print("2. Test the initial evaluation endpoint")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
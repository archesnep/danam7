from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("models", "8247_update_primary_descriptors_config"),
    ]

    sql_string = """
            CREATE OR REPLACE FUNCTION refresh_geojson_geometries() RETURNS BOOLEAN AS $$
                    BEGIN
                        TRUNCATE TABLE geojson_geometries;

                        INSERT INTO geojson_geometries(
                            tileid,
                            resourceinstanceid,
                            nodeid,
                            geom
                        )
                        SELECT t.tileid,
                            t.resourceinstanceid,
                            n.nodeid,
                            ST_Force2D(
                                ST_Transform(
                                    ST_SetSRID(
                                        (ST_Dump(
                                            st_geomfromgeojson(
                                                (
                                                    json_array_elements(
                                                        t.tiledata::json->n.nodeid::text->'features'
                                                    )->'geometry'
                                                )::text
                                            )
                                        )).geom,
                                        4326
                                    ),
                                    3857
                                )
                            ) AS geom
                        FROM tiles t
                            LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
                        GROUP BY t.tileid, t.resourceinstanceid, n.nodeid
                        HAVING n.datatype = 'geojson-feature-collection'::text;

                        RETURN TRUE;
                    END;
            $$ LANGUAGE plpgsql;

            CREATE OR REPLACE FUNCTION refresh_tile_geojson_geometries(refreshtileid UUID) RETURNS BOOLEAN AS $$
                    BEGIN
                        DELETE FROM geojson_geometries WHERE tileid = refreshtileid;

                        INSERT INTO geojson_geometries(
                            tileid,
                            resourceinstanceid,
                            nodeid,
                            geom
                        )
                        SELECT t.tileid,
                            t.resourceinstanceid,
                            n.nodeid,
                            ST_Force2D(
                                ST_Transform(
                                    ST_SetSRID(
                                        (ST_Dump(
                                            st_geomfromgeojson(
                                                (
                                                    json_array_elements(
                                                        t.tiledata::json->n.nodeid::text->'features'
                                                    )->'geometry'
                                                )::text
                                            )
                                        )).geom,
                                        4326
                                    ),
                                    3857
                                )
                            ) AS geom
                        FROM tiles t
                            LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
                        GROUP BY t.tileid, t.resourceinstanceid, n.nodeid
                        HAVING n.datatype = 'geojson-feature-collection'::text
                            AND t.tileid = refreshtileid;

                        RETURN TRUE;
                    END;
            $$ LANGUAGE plpgsql;

            SELECT refresh_geojson_geometries();
        """

    reverse_sql_string = """
            CREATE OR REPLACE FUNCTION refresh_geojson_geometries() RETURNS BOOLEAN AS $$
                    BEGIN
                        TRUNCATE TABLE geojson_geometries;

                        INSERT INTO geojson_geometries(
                            tileid,
                            resourceinstanceid,
                            nodeid,
                            geom
                        )
                        SELECT t.tileid,
                            t.resourceinstanceid,
                            n.nodeid,
                            ST_Force2D(
                                ST_Transform(
                                    ST_SetSRID(
                                        st_geomfromgeojson(
                                            (
                                                json_array_elements(
                                                    t.tiledata::json->n.nodeid::text->'features'
                                                )->'geometry'
                                            )::text
                                        ),
                                        4326
                                    ),
                                    3857
                                )
                            ) AS geom
                        FROM tiles t
                            LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
                        WHERE n.datatype = 'geojson-feature-collection'::text;

                        RETURN TRUE;
                    END;
            $$ LANGUAGE plpgsql;

            CREATE OR REPLACE FUNCTION refresh_tile_geojson_geometries(refreshtileid UUID) RETURNS BOOLEAN AS $$
                    BEGIN
                        DELETE FROM geojson_geometries WHERE tileid = refreshtileid;

                        INSERT INTO geojson_geometries(
                            tileid,
                            resourceinstanceid,
                            nodeid,
                            geom
                        )
                        SELECT t.tileid,
                            t.resourceinstanceid,
                            n.nodeid,
                            ST_Force2D(
                                ST_Transform(
                                    ST_SetSRID(
                                        st_geomfromgeojson(
                                            (
                                                json_array_elements(
                                                    t.tiledata::json->n.nodeid::text->'features'
                                                )->'geometry'
                                            )::text
                                        ),
                                        4326
                                    ),
                                    3857
                                )
                            ) AS geom
                        FROM tiles t
                            LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
                        WHERE n.datatype = 'geojson-feature-collection'::text
                        AND t.tileid = refreshtileid;

                        RETURN TRUE;
                    END;
            $$ LANGUAGE plpgsql;

            SELECT refresh_geojson_geometries();
        """

    operations = [
        migrations.RunSQL(sql_string, reverse_sql_string),
    ]

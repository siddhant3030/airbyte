/*
 * Copyright (c) 2022 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.test.utils;

public record SchemaTableNamePair(String schemaName, String tableName) {

  public String getFullyQualifiedTableName() {
    return schemaName + "." + tableName;
  }

}
